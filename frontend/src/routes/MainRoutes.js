import { lazy } from 'react';

// project-imports
import MainLayout from 'layout/MainLayout';
import CommonLayout from 'layout/CommonLayout';
import Loadable from 'components/Loadable';
import AuthGuard from 'utils/route-guard/AuthGuard';

//render - predictions
const Results = Loadable(lazy(() => import('pages/predictions/results')));
const UploadCSV = Loadable(lazy(() => import('pages/predictions/upload-csv')));

// pages routing
const MaintenanceError = Loadable(lazy(() => import('pages/maintenance/error/404')));
const MaintenanceError500 = Loadable(lazy(() => import('pages/maintenance/error/500')));

// landing page
const Landing = Loadable(lazy(() => import('pages/landing')));

// ==============================|| MAIN ROUTES ||============================== //

const MainRoutes = {
  path: '/',
  children: [
    {
      path: '/',
      element: (
        <AuthGuard>
          <MainLayout />
        </AuthGuard>
      ),
      children: [
        {
          path: 'predictions',
          children: [
            {
              path: 'upload-csv',
              element: <UploadCSV />
            },
            {
              path: 'results',
              element: <Results />
            }
          ]
        }
      ]
    },
    {
      path: '/',
      element: <CommonLayout layout="landing" />,
      children: [
        {
          path: 'landing',
          element: <Landing />
        }
      ]
    },
    {
      path: '/maintenance',
      element: <CommonLayout />,
      children: [
        {
          path: '404',
          element: <MaintenanceError />
        },
        {
          path: '500',
          element: <MaintenanceError500 />
        }
      ]
    }
  ]
};

export default MainRoutes;
