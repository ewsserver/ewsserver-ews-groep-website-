import { defineConfig } from "cf/config";

export default defineConfig({
  // Cloudflare Builds supplies the account through CLOUDFLARE_ACCOUNT_ID.
  worker: {
    name: "ews-groep-website",
    compatibilityDate: "2026-11-26",
    workersDev: true,
    previewUrls: false,
  },
});
