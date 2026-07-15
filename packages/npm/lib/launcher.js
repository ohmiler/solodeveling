"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const https = require("node:https");
const { spawn } = require("node:child_process");
const { pipeline } = require("node:stream/promises");

const REPOSITORY = "ohmiler/solodeveling";
const PLATFORM_NAMES = Object.freeze({
  "win32-x64": "windows-x64",
  "win32-arm64": "windows-arm64",
  "darwin-x64": "macos-x64",
  "darwin-arm64": "macos-arm64",
  "linux-x64": "linux-x64",
  "linux-arm64": "linux-arm64",
});
const DIGEST_PATTERN = /^[0-9a-f]{64}$/;
const VERSION_PATTERN = /^[0-9]+[.][0-9]+[.][0-9]+(?:[-+][0-9A-Za-z.-]+)?$/;
const FILE_PATTERN = /^solodeveling-[0-9A-Za-z.+-]+-(windows|macos|linux)-(x64|arm64)(?:[.]exe)?$/;

class LauncherError extends Error {}

function platformKey(platform = process.platform, arch = process.arch) {
  const key = platform + "-" + arch;
  if (!Object.hasOwn(PLATFORM_NAMES, key)) {
    throw new LauncherError(
      "unsupported platform " + key + "; install the Python package with " +
        "'uv tool install solodeveling' or 'pipx install solodeveling'",
    );
  }
  return key;
}

function expectedFilename(version, key) {
  const suffix = key.startsWith("win32-") ? ".exe" : "";
  return "solodeveling-" + version + "-" + PLATFORM_NAMES[key] + suffix;
}

function validateManifest(manifest, packageVersion, key) {
  if (!manifest || manifest.schema !== 1 || manifest.version !== packageVersion) {
    throw new LauncherError("artifact manifest does not match this npm package");
  }
  if (!VERSION_PATTERN.test(packageVersion)) {
    throw new LauncherError("npm package version is invalid");
  }
  const record = manifest.artifacts && manifest.artifacts[key];
  if (!record || typeof record !== "object") {
    throw new LauncherError(
      "native artifact for " + key + " is not included in this release; " +
        "use 'uv tool install solodeveling' or 'pipx install solodeveling'",
    );
  }
  const filename = expectedFilename(packageVersion, key);
  if (
    record.filename !== filename ||
    !FILE_PATTERN.test(record.filename) ||
    path.basename(record.filename) !== record.filename
  ) {
    throw new LauncherError("artifact filename is unsafe or does not match the release");
  }
  if (!DIGEST_PATTERN.test(record.sha256)) {
    throw new LauncherError("artifact SHA-256 is invalid");
  }
  if (!Number.isSafeInteger(record.size) || record.size <= 0) {
    throw new LauncherError("artifact size is invalid");
  }
  return Object.freeze({
    filename: record.filename,
    sha256: record.sha256,
    size: record.size,
  });
}

async function digestFile(filename) {
  const hash = crypto.createHash("sha256");
  let size = 0;
  const stream = fs.createReadStream(filename);
  for await (const chunk of stream) {
    size += chunk.length;
    hash.update(chunk);
  }
  return { sha256: hash.digest("hex"), size };
}

async function isVerified(filename, record) {
  try {
    const before = await fs.promises.lstat(filename);
    if (!before.isFile() || before.isSymbolicLink()) return false;
    const actual = await digestFile(filename);
    const after = await fs.promises.lstat(filename);
    return (
      after.isFile() &&
      !after.isSymbolicLink() &&
      before.dev === after.dev &&
      before.ino === after.ino &&
      before.size === after.size &&
      before.mtimeMs === after.mtimeMs &&
      actual.size === record.size &&
      actual.sha256 === record.sha256
    );
  } catch (error) {
    if (error && error.code === "ENOENT") return false;
    throw error;
  }
}

function releaseUrl(version, filename) {
  return (
    "https://github.com/" + REPOSITORY + "/releases/download/v" +
    encodeURIComponent(version) + "/" + encodeURIComponent(filename)
  );
}

function openHttps(url, redirects = 0) {
  if (redirects > 5) {
    return Promise.reject(new LauncherError("too many artifact download redirects"));
  }
  const parsed = new URL(url);
  if (parsed.protocol !== "https:") {
    return Promise.reject(new LauncherError("artifact download requires HTTPS"));
  }
  return new Promise((resolve, reject) => {
    const request = https.get(parsed, { headers: { "user-agent": "solodeveling-npm" } });
    request.on("response", (response) => {
      if (
        response.statusCode >= 300 &&
        response.statusCode < 400 &&
        response.headers.location
      ) {
        response.resume();
        const redirected = new URL(response.headers.location, parsed);
        openHttps(redirected, redirects + 1).then(resolve, reject);
        return;
      }
      if (response.statusCode !== 200) {
        response.resume();
        reject(
          new LauncherError("artifact download failed with HTTP " + response.statusCode),
        );
        return;
      }
      resolve(response);
    });
    request.on("error", reject);
    request.setTimeout(30000, () => {
      request.destroy(new LauncherError("artifact download timed out"));
    });
  });
}

async function downloadTo(url, destination, expectedSize) {
  const response = await openHttps(url);
  const length = response.headers["content-length"];
  if (length !== undefined && Number(length) !== expectedSize) {
    response.resume();
    throw new LauncherError("artifact download size does not match the manifest");
  }
  let received = 0;
  response.on("data", (chunk) => {
    received += chunk.length;
    if (received > expectedSize) {
      response.destroy(new LauncherError("artifact download exceeded expected size"));
    }
  });
  await pipeline(response, fs.createWriteStream(destination, { flags: "wx" }));
  if (received !== expectedSize) {
    throw new LauncherError("artifact download is incomplete");
  }
}

function defaultCacheRoot() {
  return (
    process.env.SOLODEVELING_CACHE_DIR ||
    path.join(os.homedir(), ".cache", "solodeveling")
  );
}

async function ensureBinary(options) {
  const {
    manifest,
    packageVersion,
    platform = process.platform,
    arch = process.arch,
    cacheRoot = defaultCacheRoot(),
    download = downloadTo,
  } = options;
  const key = platformKey(platform, arch);
  const record = validateManifest(manifest, packageVersion, key);
  const root = path.resolve(cacheRoot, packageVersion, key);
  const destination = path.join(root, record.filename);
  if (path.dirname(destination) !== root) {
    throw new LauncherError("artifact cache path escaped its version directory");
  }

  await fs.promises.mkdir(root, { recursive: true, mode: 0o700 });
  if (await isVerified(destination, record)) {
    if (platform !== "win32") await fs.promises.chmod(destination, 0o755);
    return destination;
  }

  await fs.promises.rm(destination, { force: true });
  const temporary = path.join(
    root,
    "." + record.filename + "." + process.pid + "." +
      crypto.randomBytes(8).toString("hex") + ".tmp",
  );
  try {
    await download(releaseUrl(packageVersion, record.filename), temporary, record.size);
    if (!(await isVerified(temporary, record))) {
      throw new LauncherError("artifact SHA-256 or size verification failed");
    }
    if (platform !== "win32") await fs.promises.chmod(temporary, 0o755);
    try {
      await fs.promises.rename(temporary, destination);
    } catch (error) {
      if (!error || !["EEXIST", "EPERM"].includes(error.code)) throw error;
      if (!(await isVerified(destination, record))) throw error;
    }
    if (!(await isVerified(destination, record))) {
      throw new LauncherError("cached artifact failed verification");
    }
    return destination;
  } finally {
    await fs.promises.rm(temporary, { force: true });
  }
}

function spawnBinary(executable, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(executable, args, {
      stdio: "inherit",
      shell: false,
      windowsHide: true,
    });
    child.on("error", reject);
    child.on("exit", (code, signal) => {
      if (signal) {
        reject(new LauncherError("native command terminated by signal " + signal));
        return;
      }
      resolve(code === null ? 1 : code);
    });
  });
}

async function run(args, options) {
  const executable = await ensureBinary(options);
  const execute = options.spawnBinary || spawnBinary;
  return execute(executable, args);
}

module.exports = {
  LauncherError,
  digestFile,
  ensureBinary,
  expectedFilename,
  platformKey,
  releaseUrl,
  run,
  validateManifest,
};
