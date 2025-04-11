import { spawnSync } from 'child_process';
import path from 'path';
import type { Plugin } from '@docusaurus/types';

export default function generateDocsPlugin(context: any, options: any): Plugin<void> {
  let hasRun = false;

  const runPythonScript = () => {
    if (hasRun) {
      console.log('Python script already executed, skipping...');
      return;
    }

    hasRun = true;
    const result = spawnSync('python3', [
      path.join(context.siteDir, 'scripts/generate_docs.py')
    ]);

    if (result.error) {
      throw new Error(`Failed to start Python script: ${result.error.message}`);
    }

    if (result.status !== 0) {
      throw new Error(`Python script exited with code ${result.status}`);
    }

    // Log output for debugging
    if (result.stdout) {
      console.log(`Python output: ${result.stdout.toString()}`);
    }
    if (result.stderr) {
      console.error(`Python error: ${result.stderr.toString()}`);
    }
  };

  return {
    name: 'docusaurus-plugin-generate-docs',
    
    loadContent(): void {
      try {
        runPythonScript();
      } catch (error) {
        console.error('Error in loadContent:', error);
        throw error;
      }
    },
  };
} 