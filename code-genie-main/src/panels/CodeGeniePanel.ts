import { Disposable, Webview, WebviewPanel, window, Uri, ViewColumn } from "vscode";
import { getNonce, getUri } from "../utilities";
const { spawn } = require('child_process');
const path = require('path');

/**
 * This class manages the state and behavior of HelloWorld webview panels.
 */
export class CodeGeniePanel {
  public static currentPanel: CodeGeniePanel | undefined;
  private readonly _panel: WebviewPanel;
  private _disposables: Disposable[] = [];

  private constructor(panel: WebviewPanel, extensionUri: Uri) {
    this._panel = panel;
    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    this._panel.webview.html = this._getWebviewContent(this._panel.webview, extensionUri);
    this._setWebviewMessageListener(this._panel.webview);
  }

  public static render(extensionUri: Uri) {
    if (CodeGeniePanel.currentPanel) {
      CodeGeniePanel.currentPanel._panel.reveal(ViewColumn.One);
    } else {
      const panel = window.createWebviewPanel(
        "Code Genie View",
        "Code Genie View",
        ViewColumn.One,
        {
          enableScripts: true,
          localResourceRoots: [Uri.joinPath(extensionUri, "out"), Uri.joinPath(extensionUri, "webview-ui/build")],
        }
      );
      CodeGeniePanel.currentPanel = new CodeGeniePanel(panel, extensionUri);
    }
  }

  public dispose() {
    CodeGeniePanel.currentPanel = undefined;
    this._panel.dispose();
    while (this._disposables.length) {
      const disposable = this._disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
  }

  private _getWebviewContent(webview: Webview, extensionUri: Uri) {
    const stylesUri = getUri(webview, extensionUri, ["webview-ui", "build", "assets", "index.css"]);
    const scriptUri = getUri(webview, extensionUri, ["webview-ui", "build", "assets", "index.js"]);
    const nonce = getNonce();

    return /*html*/ `
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
          <link rel="stylesheet" type="text/css" href="${stylesUri}">
          <title>Code Genie</title>
        </head>
        <body>
          <div id="root"></div>
          <script type="module" nonce="${nonce}" src="${scriptUri}"></script>
        </body>
      </html>
    `;
  }

  private _setWebviewMessageListener(webview: Webview) {
    webview.onDidReceiveMessage(
      (message: any) => {
        const command = message.command;
        const input1 = message.input1;
        const input2 = message.input2;
        const input3 = message.input3;
  
        switch (command) {
          case "ready":
            // Define the path to the batch file and arguments
            const batchFilePath = 'C:\\Users\\nisha\\OneDrive\\Desktop\\task.bat';
            const args = [input1, input2, input3];
            
            // Build the command array
            const cmdArgs = ['/k', batchFilePath, ...args];
  
            // Output command to the console for debugging
            console.log('Executing command:', `cmd.exe ${cmdArgs.join(' ')}`);
  
            // Execute the command
            const cmd = spawn('cmd.exe', cmdArgs, {
              cwd: path.dirname(batchFilePath), // Optional: change working directory
              shell: true
            });
  
            cmd.stdout.on('data', (data: Buffer) => {
              console.log(`stdout: ${data.toString()}`);
            });
  
            cmd.stderr.on('data', (data: Buffer) => {
              console.error(`stderr: ${data.toString()}`);
            });
  
            cmd.on('close', (code: number) => {
              console.log(`child process exited with code ${code}`);
            });
  
            cmd.on('error', (err: Error) => {
              console.error(`Failed to start subprocess: ${err.message}`);
            });
  
            break;
  
          // Add more cases as needed
        }
      },
      undefined,
      this._disposables
    );
  }
  
}
