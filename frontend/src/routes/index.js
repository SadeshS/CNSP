import { lazy } from 'react';
import { useRoutes } from 'react-router-dom';

// project-imports
import Loadable from 'components/Loadable';
import LoginRoutes from './LoginRoutes';
import MainRoutes from './MainRoutes';
import AuthGuard from 'utils/route-guard/AuthGuard';
import MainLayout from 'layout/MainLayout';

// render - landing page
const PagesLanding = Loadable(lazy(() => import('pages/landing')));

// ==============================|| ROUTES RENDER ||============================== //

export default function ThemeRoutes() {
  return useRoutes([
    {
      path: '/',
      element: (
        <AuthGuard>
          <MainLayout />
        </AuthGuard>
      ),
      children: [
        {
          path: '/',
          element: <PagesLanding />
        }
      ]
    },
    LoginRoutes,
    MainRoutes
  ]);
}
