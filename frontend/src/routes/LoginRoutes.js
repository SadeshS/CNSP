import { lazy } from 'react';

// project-imports
import GuestGuard from 'utils/route-guard/GuestGuard';
import CommonLayout from 'layout/CommonLayout';
import Loadable from 'components/Loadable';

// render - login
const AuthLogin = Loadable(lazy(() => import('pages/auth/login')));
const AuthRegister = Loadable(lazy(() => import('pages/auth/register')));

// ==============================|| AUTH ROUTES ||============================== //

const LoginRoutes = {
  path: '/',
  children: [
    {
      path: '/',
      element: (
        <GuestGuard>
          <CommonLayout />
        </GuestGuard>
      ),
      children: [
        {
          path: 'login',
          element: <AuthLogin />
        },
        {
          path: 'register',
          element: <AuthRegister />
        }
        // {
        //   path: 'forgot-password',
        //   element: <AuthForgotPassword />
        // },
        // {
        //   path: 'reset-password',
        //   element: <AuthResetPassword />
        // }
      ]
    }
  ]
};

export default LoginRoutes;
