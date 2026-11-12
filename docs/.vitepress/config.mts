import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'MaTiSSe',
  description: 'Markdown To Impressive Scientific Slides — LaTeX math, syntax highlighting, and rich layouts from plain Markdown',
  base: '/MaTiSSe/',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/MaTiSSe/favicon.svg', media: '(prefers-color-scheme: light)' }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/MaTiSSe/favicon-dark.svg', media: '(prefers-color-scheme: dark)' }],
    ['link', { rel: 'icon', href: '/MaTiSSe/favicon.ico', sizes: '48x48' }],
    ['link', { rel: 'apple-touch-icon', href: '/MaTiSSe/apple-touch-icon.png' }],
    ['meta', { name: 'theme-color', content: '#f3ede1', media: '(prefers-color-scheme: light)' }],
    ['meta', { name: 'theme-color', content: '#0c0b14', media: '(prefers-color-scheme: dark)' }],
  ],
  markdown: {
    math: true,
  },
  vite: {
    build: {
      target: 'esnext',
    },
    optimizeDeps: {
      esbuildOptions: {
        target: 'esnext',
      },
    },
  },
  themeConfig: {
    logo: { light: '/logo-mark.svg', dark: '/logo-mark-dark.svg', alt: 'MaTiSSe' },

    nav: [
      { text: 'Home', link: '/' },
      {
        text: 'Guide',
        items: [
          { text: 'About',        link: '/guide/' },
          { text: 'Installation', link: '/guide/installation' },
          { text: 'Quick Start',  link: '/guide/quickstart' },
          { text: 'Core Concepts', link: '/guide/concepts' },
          { text: 'Usage',        link: '/guide/usage' },
          { text: 'Themes',       link: '/guide/themes' },
          { text: 'Examples',     link: '/guide/examples' },
          { text: 'FAQ',          link: '/guide/faq' },
          { text: 'Changelog',    link: '/guide/changelog' },
          { text: 'Contributing', link: '/guide/contributing' },
        ],
      },
      { text: 'Reference', link: '/reference/' },
      { text: 'Advanced',  link: '/advanced/' },
      { text: 'GitHub',    link: 'https://github.com/szaghi/MaTiSSe' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Introduction',
          items: [
            { text: 'About MaTiSSe',  link: '/guide/' },
            { text: 'Installation',   link: '/guide/installation' },
            { text: 'Quick Start',    link: '/guide/quickstart' },
            { text: 'Core Concepts',  link: '/guide/concepts' },
            { text: 'Usage',          link: '/guide/usage' },
            { text: 'Themes',         link: '/guide/themes' },
            { text: 'Examples',       link: '/guide/examples' },
            { text: 'FAQ',            link: '/guide/faq' },
          ],
        },
        {
          text: 'Project',
          items: [
            { text: 'Changelog',    link: '/guide/changelog' },
            { text: 'Contributing', link: '/guide/contributing' },
          ],
        },
      ],

      '/reference/': [
        {
          text: 'CLI',
          items: [
            { text: 'Overview',        link: '/reference/' },
            { text: 'Command Options', link: '/reference/cli' },
          ],
        },
        {
          text: 'Markdown Extensions',
          items: [
            { text: 'Syntax Overview', link: '/reference/markdown-syntax' },
            { text: 'Theme YAML',      link: '/reference/themes' },
            { text: 'Metadata',        link: '/reference/metadata' },
          ],
        },
        {
          text: 'Quick Lookup',
          items: [
            { text: 'Feature Matrix',  link: '/reference/feature-matrix' },
          ],
        },
      ],

      '/advanced/': [
        {
          text: 'Overview',
          items: [
            { text: 'Advanced Topics', link: '/advanced/' },
          ],
        },
        {
          text: 'Content Environments',
          items: [
            { text: 'Figures',       link: '/advanced/figures' },
            { text: 'Boxes & Notes', link: '/advanced/boxes' },
            { text: 'Tables',        link: '/advanced/tables' },
            { text: 'Columns',       link: '/advanced/columns' },
            { text: 'Video',         link: '/advanced/video' },
            { text: 'Checklists',    link: '/advanced/checklists' },
          ],
        },
        {
          text: 'Advanced Syntax',
          items: [
            { text: 'Callout Blocks',       link: '/advanced/callouts' },
            { text: 'Theorems & Proofs',    link: '/advanced/theorems' },
            { text: 'Diagrams',             link: '/advanced/diagrams' },
            { text: 'Incremental Reveals',  link: '/advanced/incremental' },
          ],
        },
        {
          text: 'Text Formatting',
          items: [
            { text: 'Inline Formatting', link: '/advanced/inline-formatting' },
          ],
        },
        {
          text: 'Scientific Content',
          items: [
            { text: 'Math & LaTeX',      link: '/advanced/math' },
            { text: 'Code Highlighting', link: '/advanced/code' },
          ],
        },
        {
          text: 'Themes',
          items: [
            { text: 'Themes In Depth', link: '/advanced/themes' },
          ],
        },
        {
          text: 'Backends',
          items: [
            { text: 'reveal.js backend', link: '/advanced/reveal' },
            { text: 'Offline Mode',      link: '/advanced/offline' },
          ],
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/szaghi/MaTiSSe' },
    ],

    search: {
      provider: 'local',
    },

    footer: {
      message: 'Released under the <a href="http://www.gnu.org/licenses/gpl-3.0.html">GPL v3 License</a>.',
      copyright: 'Copyright © Stefano Zaghi',
    },
  },
})
