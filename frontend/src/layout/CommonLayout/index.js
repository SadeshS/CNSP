import PropTypes from 'prop-types';

import { Outlet } from 'react-router-dom';

// ==============================|| MINIMAL LAYOUT ||============================== //

const CommonLayout = ({ layout = 'blank' }) => {
  return <>{layout === 'blank' && <Outlet />}</>;
};

CommonLayout.propTypes = {
  layout: PropTypes.string
};

export default CommonLayout;
