const path = require('path');

module.exports = (context, options) => {
  return {
    name: 'docusaurus-plugin-rag-chatbot',

    getClientModules() {
      return [path.resolve(__dirname, './src/client/module')];
    },

    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@rag-chatbot': path.resolve(__dirname, './src'),
          },
        },
      };
    },

    plugins: [
      [
        '@docusaurus/plugin-content-pages',
        {
          path: path.resolve(__dirname, './pages'),
          routeBasePath: 'rag-chatbot',
        },
      ],
    ],

    // Add the chatbot component to the right sidebar of all pages
    injectHtmlTags() {
      return {
        postBodyTags: [
          `<div id="rag-chatbot-root"></div>`,
        ],
      };
    },
  };
};