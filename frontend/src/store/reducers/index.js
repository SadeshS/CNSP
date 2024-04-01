// third-party
import { combineReducers } from 'redux';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

// project-imports
import menuReducer from './menu';
import snackbar from './snackbar';

// ==============================|| COMBINE REDUCERS ||============================== //

const reducers = combineReducers({
  snackbar,
  menu: persistReducer(
    {
      key: 'menu',
      storage,
      keyPrefix: 'cnsp-ts-'
    },
    menuReducer
  )
});

export default reducers;
