export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);

    if (response.status !== 404 || !["GET", "HEAD"].includes(request.method)) {
      return response;
    }

    const fallbackUrl = new URL(request.url);
    fallbackUrl.pathname = fallbackUrl.pathname.endsWith("/")
      ? `${fallbackUrl.pathname}index.html`
      : `${fallbackUrl.pathname}/index.html`;

    const fallback = await env.ASSETS.fetch(new Request(fallbackUrl, request));
    return fallback.status === 404 ? response : fallback;
  }
};
