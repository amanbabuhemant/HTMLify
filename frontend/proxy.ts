import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import {
  AUTH_ONLY_ROUTES,
  PROTECTED_ROUTES,
  DASHBOARD_ROUTES,
  handleAuthOrProtectedRoute,
} from "@/lib/modules/auth/auth.proxy";
import { serverFile } from "@/lib/modules/file/file.proxy";
import { serverPenContent } from "@/lib/modules/pen/pen.proxy";
import { excludePaths } from "@/lib/modules/proxy/proxy.config";
import { serveShortlink } from "@/lib/modules/shortlink/shortlink.proxy";
import { serveTmpFile } from "@/lib/modules/tmp/tmp.proxy";

import { env } from "./lib/env";

const shortnerPaths = ["/r"];
const tmpPaths = ["/tmp"];
const penPaths = ["/pen"];
const matchRoute = (route: string, routes: string[]) =>
  routes.some((r) => route === r || route.startsWith(r + "/"));

const isTmp = (pathname: string) => matchRoute(pathname, tmpPaths);
const isShortLink = (pathname: string) => matchRoute(pathname, shortnerPaths);
const isPen = (pathname: string) => matchRoute(pathname, penPaths);
const isDashboardRoute = (pathname: string) => matchRoute(pathname, DASHBOARD_ROUTES);

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hostname = request.headers.get("host")?.split(":")[0] ?? "";
  const siteUrl = new URL(env.NEXT_PUBLIC_SITE_URL);
  const publicHostname = siteUrl.hostname;
  const dashboardHostname = `${env.NEXT_PUBLIC_SUBDOMAIN}.${publicHostname}`;

  if (hostname === publicHostname && isDashboardRoute(pathname)) {
    const url = request.nextUrl.clone();
    url.hostname = dashboardHostname;
    return NextResponse.redirect(url);
  }

  if (pathname === "/api") {
    return NextResponse.redirect(`${env.NEXT_PUBLIC_BACKEND_API_URL}/docs`);
  }

  if (isShortLink(pathname)) {
    const redirect = await serveShortlink(pathname);
    if (redirect) {
      return redirect;
    }
  }

  if (isPen(pathname)) {
    const id = pathname.split("/")[2];
    if (id) {
      return await serverPenContent(id);
    }
  }

  if (excludePaths.some((path) => pathname.startsWith(path))) {
    return NextResponse.next();
  }

  const totalExcludeRoute = AUTH_ONLY_ROUTES.concat(PROTECTED_ROUTES);

  if (totalExcludeRoute.some((path: string) => pathname.startsWith(path))) {
    return await handleAuthOrProtectedRoute(request, pathname);
  }

  if (isTmp(pathname)) {
    const id = pathname.split("/")[2];
    if (id && id !== "f") {
      return await serveTmpFile(id);
    }
    return;
  }

  return await serverFile(pathname);
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|\\.well-known|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico|css|js|woff|woff2)$).*)",
    "/((?!about).*)",
  ],
};
