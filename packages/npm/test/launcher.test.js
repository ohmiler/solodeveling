"use strict";

const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");

const {
  LauncherError,
  ensureBinary,
  expectedFilename,
  platformKey,
  releaseUrl,
  run,
  validateManifest,
} = require("../lib/launcher");

function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function fixture(bytes = Buffer.from("verified-native")) {
  const version = "0.1.0";
  const key = "linux-x64";
  return {
    bytes,
    key,
    version,
    manifest: {
      schema: 1,
      version,
      artifacts: {
        [key]: {
          filename: expectedFilename(version, key),
          sha256: sha256(bytes),
          size: bytes.length,
        },
      },
    },
  };
}

test("package exposes one public name without lifecycle scripts or dependencies", () => {
  const metadata = require("../package.json");

  assert.equal(metadata.name, "solodeveling");
  assert.deepEqual(metadata.bin, { solodeveling: "bin/solodeveling.js" });
  assert.equal(metadata.dependencies, undefined);
  for (const lifecycle of ["preinstall", "install", "postinstall"]) {
    assert.equal(metadata.scripts[lifecycle], undefined);
  }
});

test("platform mapping is explicit and unsupported targets fail closed", () => {
  assert.equal(platformKey("win32", "x64"), "win32-x64");
  assert.equal(platformKey("darwin", "arm64"), "darwin-arm64");
  assert.throws(
    () => platformKey("freebsd", "x64"),
    (error) =>
      error instanceof LauncherError &&
      error.message.includes("unsupported platform freebsd-x64"),
  );
});

test("manifest binds exact package version, safe filename, hash, and size", () => {
  const data = fixture();
  assert.deepEqual(
    validateManifest(data.manifest, data.version, data.key),
    data.manifest.artifacts[data.key],
  );

  const wrongVersion = structuredClone(data.manifest);
  wrongVersion.version = "0.1.1";
  assert.throws(
    () => validateManifest(wrongVersion, data.version, data.key),
    /does not match/,
  );

  const traversal = structuredClone(data.manifest);
  traversal.artifacts[data.key].filename = "../solodeveling.exe";
  assert.throws(
    () => validateManifest(traversal, data.version, data.key),
    /filename is unsafe/,
  );

  const badHash = structuredClone(data.manifest);
  badHash.artifacts[data.key].sha256 = "0".repeat(63);
  assert.throws(
    () => validateManifest(badHash, data.version, data.key),
    /SHA-256 is invalid/,
  );

  const badSize = structuredClone(data.manifest);
  badSize.artifacts[data.key].size = 0;
  assert.throws(
    () => validateManifest(badSize, data.version, data.key),
    /size is invalid/,
  );
});

test("release URL is immutable and encodes the exact version and filename", () => {
  assert.equal(
    releaseUrl("0.1.0", "solodeveling-0.1.0-linux-x64"),
    "https://github.com/ohmiler/solodeveling/releases/download/" +
      "v0.1.0/solodeveling-0.1.0-linux-x64",
  );
});

test("verified download is cached and reused", async (t) => {
  const data = fixture();
  const cacheRoot = await fs.promises.mkdtemp(
    path.join(os.tmpdir(), "solodeveling-launcher-"),
  );
  t.after(() => fs.promises.rm(cacheRoot, { recursive: true, force: true }));
  let downloads = 0;
  const download = async (url, destination, size) => {
    downloads += 1;
    assert.equal(url, releaseUrl(data.version, expectedFilename(data.version, data.key)));
    assert.equal(size, data.bytes.length);
    await fs.promises.writeFile(destination, data.bytes, { flag: "wx" });
  };
  const options = {
    manifest: data.manifest,
    packageVersion: data.version,
    platform: "linux",
    arch: "x64",
    cacheRoot,
    download,
  };

  const first = await ensureBinary(options);
  const second = await ensureBinary(options);

  assert.equal(first, second);
  assert.equal(downloads, 1);
  assert.deepEqual(await fs.promises.readFile(first), data.bytes);
});

test("tampered cache is replaced and verified before execution", async (t) => {
  const data = fixture();
  const cacheRoot = await fs.promises.mkdtemp(
    path.join(os.tmpdir(), "solodeveling-tamper-"),
  );
  t.after(() => fs.promises.rm(cacheRoot, { recursive: true, force: true }));
  const destination = path.join(
    cacheRoot,
    data.version,
    data.key,
    expectedFilename(data.version, data.key),
  );
  await fs.promises.mkdir(path.dirname(destination), { recursive: true });
  await fs.promises.writeFile(destination, "tampered");

  let downloads = 0;
  const result = await ensureBinary({
    manifest: data.manifest,
    packageVersion: data.version,
    platform: "linux",
    arch: "x64",
    cacheRoot,
    download: async (_url, temporary) => {
      downloads += 1;
      await fs.promises.writeFile(temporary, data.bytes, { flag: "wx" });
    },
  });

  assert.equal(downloads, 1);
  assert.equal(result, destination);
  assert.deepEqual(await fs.promises.readFile(result), data.bytes);
});

test("cached symlinks are never accepted as executable artifacts", async (t) => {
  const data = fixture();
  const cacheRoot = await fs.promises.mkdtemp(
    path.join(os.tmpdir(), "solodeveling-symlink-"),
  );
  t.after(() => fs.promises.rm(cacheRoot, { recursive: true, force: true }));
  const outside = path.join(cacheRoot, "outside");
  await fs.promises.writeFile(outside, data.bytes);
  const destination = path.join(
    cacheRoot,
    data.version,
    data.key,
    expectedFilename(data.version, data.key),
  );
  await fs.promises.mkdir(path.dirname(destination), { recursive: true });
  try {
    await fs.promises.symlink(outside, destination, "file");
  } catch (error) {
    if (error && ["EPERM", "EACCES"].includes(error.code)) {
      t.skip("file symlinks are unavailable in this environment");
      return;
    }
    throw error;
  }
  let downloads = 0;

  const resolved = await ensureBinary({
    manifest: data.manifest,
    packageVersion: data.version,
    platform: "linux",
    arch: "x64",
    cacheRoot,
    download: async (_url, temporary) => {
      downloads += 1;
      await fs.promises.writeFile(temporary, data.bytes, { flag: "wx" });
    },
  });

  assert.equal(downloads, 1);
  assert.equal((await fs.promises.lstat(resolved)).isSymbolicLink(), false);
  assert.deepEqual(await fs.promises.readFile(outside), data.bytes);
});

test("hash mismatch never reaches the executable boundary", async (t) => {
  const data = fixture();
  const cacheRoot = await fs.promises.mkdtemp(
    path.join(os.tmpdir(), "solodeveling-mismatch-"),
  );
  t.after(() => fs.promises.rm(cacheRoot, { recursive: true, force: true }));
  let spawned = false;

  await assert.rejects(
    run(["version"], {
      manifest: data.manifest,
      packageVersion: data.version,
      platform: "linux",
      arch: "x64",
      cacheRoot,
      download: async (_url, temporary) => {
        await fs.promises.writeFile(temporary, "malicious", { flag: "wx" });
      },
      spawnBinary: async () => {
        spawned = true;
        return 0;
      },
    }),
    /verification failed/,
  );
  assert.equal(spawned, false);
});

test("arguments and native exit code are passed through without a shell", async (t) => {
  const data = fixture();
  const cacheRoot = await fs.promises.mkdtemp(
    path.join(os.tmpdir(), "solodeveling-spawn-"),
  );
  t.after(() => fs.promises.rm(cacheRoot, { recursive: true, force: true }));
  let invocation;

  const code = await run(["install", "--runtime", "codex"], {
    manifest: data.manifest,
    packageVersion: data.version,
    platform: "linux",
    arch: "x64",
    cacheRoot,
    download: async (_url, temporary) => {
      await fs.promises.writeFile(temporary, data.bytes, { flag: "wx" });
    },
    spawnBinary: async (executable, args) => {
      invocation = { executable, args };
      return 19;
    },
  });

  assert.equal(code, 19);
  assert.deepEqual(invocation.args, ["install", "--runtime", "codex"]);
  assert.equal(path.basename(invocation.executable), expectedFilename(data.version, data.key));
});
