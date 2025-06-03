// platform-web.js
export const Platform = {
    OS: 'web',
    select: (platforms) => platforms.web || platforms.default,
};