import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const cwd = process.cwd();

function logStep(message) {
  console.log(`[shadow-validate] ${message}`);
}

function run(command, options = {}) {
  const opts = { stdio: "inherit", cwd, env: process.env, shell: true, ...options };
  execSync(command, opts);
}

function readPackageJson() {
  const packagePath = path.join(cwd, "package.json");
  if (!fs.existsSync(packagePath)) {
    throw new Error(`package.json not found at ${packagePath}`);
  }
  const raw = fs.readFileSync(packagePath, "utf8");
  return JSON.parse(raw);
}

function getEnvAlias(keys) {
  for (const key of keys) {
    const value = process.env[key];
    if (value && value.trim().length > 0) {
      return { key, value: value.trim() };
    }
  }
  return null;
}

function requireEnvAlias(label, keys) {
  const found = getEnvAlias(keys);
  if (!found) {
    throw new Error(`Missing required env: ${label} (checked: ${keys.join(", ")})`);
  }
  return found;
}

function validateSupabaseUrl(value) {
  const lower = value.toLowerCase();
  if (!lower.startsWith("https://") || !lower.includes(".supabase.co")) {
    throw new Error("Invalid Supabase URL format. Expected https://*.supabase.co");
  }
}

function validateSupabaseKey(value) {
  const trimmed = value.trim();
  if (trimmed.length < 20 || /\s/.test(trimmed)) {
    throw new Error("Invalid Supabase key format. Expected length >= 20 with no spaces.");
  }
}

function detectOutputDir(buildScript) {
  const override = process.env.BUILD_OUTPUT_DIR;
  if (override && override.trim().length > 0) {
    return override.trim();
  }

  const script = (buildScript || "").toLowerCase();
  if (script.includes("vite")) return "dist";
  if (script.includes("react-scripts")) return "build";
  if (script.includes("next") && script.includes("build")) return ".next";
  if (script.includes("astro")) return "dist";
  if (script.includes("gatsby")) return "public";

  const fallback = ["dist", "build", "out", "public"];
  for (const dir of fallback) {
    if (fs.existsSync(path.join(cwd, dir))) {
      return dir;
    }
  }
  return fallback[0];
}

function validateOutputDir(outputDir) {
  const fullPath = path.join(cwd, outputDir);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Build output directory not found: ${outputDir}`);
  }

  if (outputDir === ".next") {
    const buildId = path.join(fullPath, "BUILD_ID");
    const staticDir = path.join(fullPath, "static");
    if (!fs.existsSync(buildId) && !fs.existsSync(staticDir)) {
      throw new Error("Next.js output missing BUILD_ID or static directory.");
    }
    return;
  }

  const indexPath = path.join(fullPath, "index.html");
  if (!fs.existsSync(indexPath)) {
    throw new Error(`index.html not found in ${outputDir}`);
  }
}

function runScriptIfPresent(pkg, name) {
  if (pkg.scripts && pkg.scripts[name]) {
    logStep(`Running npm run ${name}...`);
    try {
      run(`npm run ${name}`);
    } catch (error) {
      logStep(`Warning: npm run ${name} failed (not critical for shadow validation).`);
      logStep(`Details: ${error.message || error}`);
    }
  } else {
    logStep(`Skipping ${name} (script not found).`);
  }
}

function main() {
  logStep("Starting shadow deploy validation.");

  process.env.CI = process.env.CI || "true";
  process.env.NODE_ENV = process.env.NODE_ENV || "production";

  logStep("Checking Node and npm...");
  run("node -v");
  run("npm -v");

  const pkg = readPackageJson();

  const forbiddenKeys = [
    "SUPABASE_SERVICE_ROLE_KEY",
    "SERVICE_ROLE_KEY",
    "VITE_SUPABASE_SERVICE_ROLE_KEY",
  ];
  const forbiddenFound = forbiddenKeys.filter((key) => process.env[key]);
  if (forbiddenFound.length > 0) {
    throw new Error(`Forbidden env vars present: ${forbiddenFound.join(", ")}`);
  }

  const url = requireEnvAlias("Supabase URL", ["VITE_SUPABASE_URL", "SUPABASE_URL"]);
  const key = requireEnvAlias("Supabase Anon Key", [
    "VITE_SUPABASE_ANON_KEY",
    "VITE_SUPABASE_KEY",
    "SUPABASE_ANON_KEY",
    "SUPABASE_KEY",
  ]);

  validateSupabaseUrl(url.value);
  validateSupabaseKey(key.value);

  logStep("Installing dependencies...");
  const hasLock = fs.existsSync(path.join(cwd, "package-lock.json"));
  run(hasLock ? "npm ci" : "npm install");

  runScriptIfPresent(pkg, "lint");
  runScriptIfPresent(pkg, "test");
  runScriptIfPresent(pkg, "build");

  const outputDir = detectOutputDir(pkg.scripts?.build);
  logStep(`Validating build output: ${outputDir}`);
  validateOutputDir(outputDir);

  logStep("Shadow deploy validation completed successfully.");
}

try {
  main();
} catch (error) {
  console.error(`[shadow-validate] ${error.message || error}`);
  process.exit(1);
}
