#!/usr/bin/env node
/**
 * validate-shadow-deploy.mjs
 * 
 * Frontend Shadow Environment Validator
 * Enforces Supabase configuration security for shadow deployment
 * 
 * Usage:
 *   VITE_SUPABASE_URL=<url> VITE_SUPABASE_ANON_KEY=<key> node validate-shadow-deploy.mjs
 *   npm run validate:shadow (if configured in package.json)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Color codes for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkEnvironmentVariables() {
  log('\n[1/3] Checking environment variables...', 'blue');
  
  const requiredVars = [
    { name: 'VITE_SUPABASE_URL', alias: 'SUPABASE_URL' },
    { name: 'VITE_SUPABASE_ANON_KEY', alias: 'SUPABASE_ANON_KEY' },
  ];
  
  let allPresent = true;
  
  for (const { name, alias } of requiredVars) {
    const value = process.env[name] || process.env[alias];
    if (!value) {
      log(`  ✗ Missing: ${name} (or ${alias})`, 'red');
      allPresent = false;
    } else {
      log(`  ✓ Found: ${name}`, 'green');
    }
  }
  
  if (!allPresent) {
    log('\nFATAL: Required environment variables not set', 'red');
    process.exit(1);
  }
  
  return true;
}

function validateSupabaseConfig() {
  log('\n[2/3] Validating Supabase configuration...', 'blue');
  
  const anonKey = process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;
  const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
  
  // Check for service_role key (must NOT be used in frontend)
  if (anonKey.includes('service_role') || anonKey.includes('spr_')) {
    log('  ✗ SECURITY VIOLATION: Service role key detected in frontend config', 'red');
    process.exit(1);
  }
  
  // Validate Supabase URL format
  if (!url.startsWith('https://') || !url.includes('.supabase.co')) {
    log('  ✗ Invalid Supabase URL format', 'red');
    process.exit(1);
  }
  
  log('  ✓ Supabase URL format valid', 'green');
  log('  ✓ Using anon key (service role check passed)', 'green');
  
  return true;
}

function validateBuildOutput() {
  log('\n[3/3] Checking Vite build output...', 'blue');
  
  const distPath = path.join(__dirname, 'dist');
  
  if (!fs.existsSync(distPath)) {
    log(`  ⚠ Build output not found at ${distPath}`, 'yellow');
    log('  Ensure Vite build has been executed: npm run build', 'yellow');
    // Don't fail here - just warn
  } else {
    const indexPath = path.join(distPath, 'index.html');
    if (fs.existsSync(indexPath)) {
      log('  ✓ Vite dist/ directory exists with index.html', 'green');
    } else {
      log('  ⚠ dist/ exists but index.html not found', 'yellow');
    }
  }
  
  return true;
}

function main() {
  log('═══════════════════════════════════════════════════════════════', 'blue');
  log('  Frontend Shadow Environment Validator (v1.0)', 'blue');
  log('═══════════════════════════════════════════════════════════════', 'blue');
  
  try {
    checkEnvironmentVariables();
    validateSupabaseConfig();
    validateBuildOutput();
    
    log('\n═══════════════════════════════════════════════════════════════', 'green');
    log('  ✓ All validations passed!', 'green');
    log('═══════════════════════════════════════════════════════════════', 'green');
    process.exit(0);
  } catch (error) {
    log(`\n[ERROR] ${error.message}`, 'red');
    process.exit(1);
  }
}

main();
