export default {
  target: 'static',
  env: {
    baseUrl:
      process.env.NODE_ENV === 'production'
        ? 'https://akkireddy95.github.io'
        : 'http://localhost:8888'
  },
  /*
   ** Headers of the page
   */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,800;0,900;1,400&display=swap'
      }
    ]
  },
  /*
   ** Components Property
   */
  components: true,
  /*
   ** Image Property
   */
  image: {
    staticFilename: '[publicPath]/images/[name]-[hash][ext]'
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: ['@/assets/css/screen.css'],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    // Docs: https://image.nuxtjs.org/
    '@nuxt/image',
    // Docs: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
    // Docs: https://github.com/nuxt-community/analytics-module
    [
      '@nuxtjs/google-analytics',
      {
        id: 'G-3W1YEGKE7N'
      }
    ],
    // Docs: https://github.com/nuxt-community/stylelint-module
    '@nuxtjs/stylelint-module'
  ],
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxt/content',
    '@nuxt/http',
    '@nuxtjs/axios',
    '@nuxtjs/feed',
    '@nuxtjs/pwa'
  ],
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {},
  content: {
    markdown: {
      prism: {
        theme: 'prism-themes/themes/prism-night-owl.css'
      }
    }
  },
  // $http Configuration: https://go.nuxtjs.dev/config-build
  http: {
    baseUrl:
      process.env.NODE_ENV !== 'production'
        ? 'http://localhost:8888'
        : 'https://akkireddy95.github.io'
  },
  /*
   ** Feed module configuration
   ** See https://github.com/nuxt-community/feed-module
   */
  feed: [
    {
      path: '/rss.xml',
      async create(feed) {
        const { $content } = require('@nuxt/content')
        const files = await $content('blog').fetch()

        feed.options = {
          title: "Akkireddy's Blog",
          link: 'https://akkireddy95.github.io/feed.xml',
          description: 'Get the latest posts from Akkireddy'
        }

        files.forEach((post) => {
          feed.addItem({
            title: post.title,
            id: post.path,
            link: `https://akkireddy95.github.io${post.path}`,
            description: post.excerpt
          })
        })

        feed.addContributor({
          name: 'Ben Hong',
          email: 'challaakkireddy@gmail.com',
          link: 'https://akkireddy95.github.io'
        })
      },
      cacheTime: 1000 * 60 * 15,
      type: 'rss2'
    }
  ],
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {}
  },
  generate: {
    fallback: '404.html',
    async routes() {
      const { $content } = require('@nuxt/content')
      const files = await $content('blog').fetch()

      return files.map((file) => (file.path === '/index' ? '/' : file.path))
    }
  }
}
