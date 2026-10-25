import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const android = path.join(root, 'android');

async function read(rel) {
  return readFile(path.join(android, rel), 'utf8');
}
async function write(rel, content) {
  return writeFile(path.join(android, rel), content, 'utf8');
}
function requireText(content, needle, label) {
  if (!content.includes(needle)) throw new Error(`${label}: expected ${needle}`);
}
function replaceOne(content, pattern, replacement, label) {
  const next = content.replace(pattern, replacement);
  if (next === content) throw new Error(`${label}: expected patch target not found`);
  return next;
}

const variables = await read('variables.gradle');
requireText(variables, 'minSdkVersion = 24', 'variables.gradle');
requireText(variables, 'compileSdkVersion = 36', 'variables.gradle');
requireText(variables, 'targetSdkVersion = 36', 'variables.gradle');

const rootGradle = await read('build.gradle');
requireText(rootGradle, "classpath 'com.android.tools.build:gradle:8.13.0'", 'build.gradle');

const wrapper = await read('gradle/wrapper/gradle-wrapper.properties');
requireText(wrapper, 'gradle-8.14.3-all.zip', 'gradle wrapper');

const capacitorGradle = await readFile(
  path.join(root, 'node_modules', '@capacitor', 'android', 'capacitor', 'build.gradle'),
  'utf8'
);
requireText(capacitorGradle, 'sourceCompatibility JavaVersion.VERSION_21', '@capacitor/android Java source level');
requireText(capacitorGradle, 'targetCompatibility JavaVersion.VERSION_21', '@capacitor/android Java target level');

let appGradle = await read('app/build.gradle');
requireText(appGradle, 'applicationId "com.hotmoral.twindock"', 'app/build.gradle applicationId');
requireText(appGradle, 'namespace = "com.hotmoral.twindock"', 'app/build.gradle namespace');
requireText(appGradle, 'versionCode 1', 'app/build.gradle versionCode');
if (appGradle.includes('versionName "1.0"')) {
  appGradle = replaceOne(appGradle, 'versionName "1.0"', 'versionName "0.1.0"', 'versionName');
} else {
  requireText(appGradle, 'versionName "0.1.0"', 'app/build.gradle versionName');
}
await write('app/build.gradle', appGradle);

let manifest = await read('app/src/main/AndroidManifest.xml');
requireText(manifest, '<uses-permission android:name="android.permission.INTERNET" />', 'AndroidManifest INTERNET permission');

manifest = manifest.replace(/<application\b([^>]*)>/, (match, attrs) => {
  if (attrs.includes('android:appCategory=')) return match;
  return `<application${attrs}\n        android:appCategory="game">`;
});
if (!manifest.includes('android:appCategory="game"')) {
  throw new Error('AndroidManifest: failed to set app category game');
}

manifest = manifest.replace(/<activity\b([^>]*android:name="\.MainActivity"[^>]*)>/, (match, attrs) => {
  if (attrs.includes('android:screenOrientation=')) return match;
  return `<activity${attrs}\n            android:screenOrientation="sensorLandscape">`;
});
if (!manifest.includes('android:screenOrientation="sensorLandscape"')) {
  throw new Error('AndroidManifest: failed to set sensorLandscape');
}
await write('app/src/main/AndroidManifest.xml', manifest);

const mainActivityPath = 'app/src/main/java/com/hotmoral/twindock/MainActivity.java';
const mainActivity = await read(mainActivityPath);
requireText(mainActivity, 'package com.hotmoral.twindock;', 'MainActivity package');
if (mainActivity.includes('EdgeToEdge.enable(') || mainActivity.includes('WindowCompat.enableEdgeToEdge(')) {
  throw new Error('First parity probe must not force edge-to-edge on pre-Android-15 devices.');
}

console.log('Twin Dock Android template contract verified and patched.');
