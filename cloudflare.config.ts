import { defineConfig } from "cf/config";

export default defineConfig({
  accountId: "a542d2fbbdbb308d5dc826632b944bef",
  worker: {
    name: "ews-groep-website",
    compatibilityDate: "2026-11-26",
    workersDev: true,
    previewUrls: false,
  },
});
