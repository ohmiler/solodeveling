#!/usr/bin/env node
"use strict";

const manifest = require("../artifacts.json");
const packageMetadata = require("../package.json");
const { run } = require("../lib/launcher");

run(process.argv.slice(2), {
  manifest,
  packageVersion: packageMetadata.version,
}).then(
  (code) => {
    process.exitCode = code;
  },
  (error) => {
    const message = error instanceof Error ? error.message : String(error);
    console.error("solodeveling: " + message);
    process.exitCode = 1;
  },
);
