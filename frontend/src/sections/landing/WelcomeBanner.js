// material-ui
import { Grid, Typography, Stack } from '@mui/material';
import { useTheme } from '@mui/material/styles';

// project import
import MainCard from 'components/MainCard';
import { ThemeMode } from 'config';

//asset
import cardBack from 'assets/images/landing/img-dropbox-bg.svg';
import WelcomeImage from 'assets/images/landing/welcome-banner.png';

// ==============================|| WELCOME ||============================== //

const WelcomeBanner = () => {
  const theme = useTheme();

  return (
    <MainCard
      border={false}
      sx={{
        color: 'common.white',
        bgcolor: theme.palette.mode === ThemeMode.DARK ? 'primary.400' : 'primary.darker',
        '&:after': {
          content: '""',
          backgroundImage: `url(${cardBack})`,
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 1,
          opacity: 0.5,
          backgroundPosition: 'bottom right',
          backgroundSize: '100%',
          backgroundRepeat: 'no-repeat'
        }
      }}
    >
      <Grid container>
        <Grid item md={9} sm={9} xs={12}>
          <Stack spacing={2} sx={{ padding: 3 }}>
            <Typography variant="h2" color={theme.palette.background.paper}>
              CNSP: Unveiling Your Customers&apos; Next Purchase
            </Typography>
            <Typography variant="h6" color={theme.palette.background.paper}>
              Empower your retail strategy with CNSP, the innovative predictor platform designed for forward-thinking retailers. Simply
              upload your store&apos;s transaction data and discover not just what your customers will buy next, but also the quantities
              they&apos;ll need. Transform insights into action and tailor your inventory to meet demand before it even arises. With CNSP,
              you&apos;re not just stocking up; you&apos;re staying ahead.
            </Typography>
          </Stack>
        </Grid>
        <Grid item sm={3} xs={12} sx={{ display: { xs: 'none', sm: 'initial' } }}>
          <Stack sx={{ position: 'relative', pr: { sm: 3, md: 8 }, zIndex: 2 }} justifyContent="center" alignItems="flex-end">
            <img src={WelcomeImage} alt="Welcome" width="200px" />
          </Stack>
        </Grid>
      </Grid>
    </MainCard>
  );
};

export default WelcomeBanner;
