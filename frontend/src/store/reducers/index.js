// third-party
import { combineReducers } from 'redux';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

// project-imports
import menu from './menu';
import snackbar from './snackbar';
import cartReducer from './cart';

// ==============================|| COMBINE REDUCERS ||============================== //

const reducers = combineReducers({
  menu,
  snackbar,
  cart: persistReducer(
    {
      key: 'cart',
      storage,
      keyPrefix: 'able-pro-material-ts-'
    },
    cartReducer
  )
});

export default reducers;
