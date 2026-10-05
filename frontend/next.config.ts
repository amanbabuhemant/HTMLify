import type { NextConfig } from "next";

const bodySizeMB = parseInt(process.env.PROXY_MAX_BODY_SIZE_MB || "32", 10);

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    proxyClientMaxBodySize: `${bodySizeMB}mb`,
  },
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
      },
    ],
  },
  allowedDevOrigins: [
    "localhost:3000",
    "my.localhost",
    "localhost",
    "localhost:4000",
  ],
};

export default nextConfig;
