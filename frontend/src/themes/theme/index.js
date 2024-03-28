import PropTypes from 'prop-types';

// project-imports
import Default from './default';

// ==============================|| PRESET THEME - THEME SELECTOR ||============================== //

const Theme = (presetColor, mode) => {
  return Default(mode);
};

Theme.propTypes = {
  colors: PropTypes.object,
  presetColor: PropTypes.any
};

export default Theme;
