// project-imports
import { useSelector } from 'store';

// ==============================|| MENU ITEMS - API ||============================== //

export const Menu = () => {
  const { menu } = useSelector((state) => state.menu);

  const menuList = {
    ...menu
  };

  return menuList;
};
