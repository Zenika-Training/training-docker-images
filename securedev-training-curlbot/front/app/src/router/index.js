import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Reset from '../components/Reset'
import Register from '../components/Register'
import Contact from '../components/Contact'
import Profile from '../components/Profile'
import Bots from '../components/Bots'
import Bot from '../components/Bot'
import CreateBot from '../components/CreateBot'
import PublicBots from '../components/PublicBots'
import store from '../store/AuthenticationStore'
import auth from '../middleware/auth'

Vue.use(Router)
const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Login,
      meta: {
        middleware: auth,
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        middleware: auth,
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {
        middleware: auth,
      }
    },
    {
      path: '/reset',
      name: 'Reset',
      component: Reset,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: { 
        requiresAuth: true,
        layout: 'authenticated',
      }
    },
    {
      path: '/bots',
      name: 'Bots',
      component: Bots,
      meta: { 
        requiresAuth: true,
        layout: 'authenticated',
      }
    },
    { path: '/bot/:id',
      name: 'Bot',
      component: Bot,
      meta: { 
        requiresAuth: true,
        layout: 'authenticated',
      }
    },
    {
      path: '/create-bot',
      name: 'CreateBot',
      component: CreateBot,
      meta: { 
        requiresAuth: true,
        layout: 'authenticated',
      }
    },
    {
      path: '/search-bot',
      name: 'PublicBots',
      component: PublicBots,
      meta: { 
        requiresAuth: true,
        layout: 'authenticated',
      }
    },
    {
      path: '/contact',
      name: 'Contact',
      component: Contact,
    }

    
  ]
})

function nextFactory(context, middleware, index) {
  const subsequentMiddleware = middleware[index];
  // If no subsequent Middleware exists,
  // the default `next()` callback is returned.
  if (!subsequentMiddleware) return context.next;

  return (...parameters) => {
    // Run the default Vue Router `next()` callback first.
    context.next(...parameters);
    // Then run the subsequent Middleware with a new
    // `nextMiddleware()` callback.
    const nextMiddleware = nextFactory(context, middleware, index + 1);
    subsequentMiddleware({ ...context, next: nextMiddleware });
  };
}
router.beforeEach((to, from, next) => {
  if (to.meta.middleware) {
    const middleware = Array.isArray(to.meta.middleware) ? to.meta.middleware : [to.meta.middleware];
    const context = { from, next, router, to,};
    const nextMiddleware = nextFactory(context, middleware, 1);
    return middleware[0]({ ...context, next: nextMiddleware });
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next() 
  }
})
export default router;

