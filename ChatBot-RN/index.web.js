import { AppRegistry } from "react-native";
import App from "./src/App";
import { name as appName } from "./app.json";

import { createRoot } from "react-dom/client";

AppRegistry.registerComponent(appName, () => App);

const rootTag = document.getElementById("app");
const root = createRoot(rootTag);

AppRegistry.runApplication(appName, { initialProps: {}, rootTag });