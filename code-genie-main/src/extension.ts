import { commands, ExtensionContext } from "vscode";
import { CodeGeniePanel } from "./panels/CodeGeniePanel";

export function activate(context: ExtensionContext) {

  // Add command to the extension context
  context.subscriptions.push(commands.registerCommand("code-genie.run", () => {
    CodeGeniePanel.render(context.extensionUri);
  }));
}