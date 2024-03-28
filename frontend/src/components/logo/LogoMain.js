import PropTypes from 'prop-types';

// material-ui
import logo from 'assets/images/landing/logo.svg';

// ==============================|| LOGO SVG ||============================== //

const LogoMain = () => {
  return <img src={logo} alt="icon logo" width="50" />;
};

LogoMain.propTypes = {
  reverse: PropTypes.bool
};

export default LogoMain;
