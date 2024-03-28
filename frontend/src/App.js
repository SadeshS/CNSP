// project-imports
import Routes from 'routes';
import ThemeCustomization from 'themes';

import Snackbar from 'components/@extended/Snackbar';

// auth-provider
import { FirebaseProvider as AuthProvider } from 'contexts/FirebaseContext';

// ==============================|| APP - THEME, ROUTER, LOCAL  ||============================== //

const App = () => {
  return (
    <ThemeCustomization>
      <AuthProvider>
        <>
          <Routes />
          <Snackbar />
        </>
      </AuthProvider>
    </ThemeCustomization>
  );
};

export default App;
