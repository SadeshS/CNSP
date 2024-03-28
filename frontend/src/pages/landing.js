// material-ui
import { Grid } from '@mui/material';

// assets
import WelcomeBanner from 'sections/landing/WelcomeBanner';

// ==============================|| Landing ||============================== //

const Landing = () => {
  return (
    <Grid container rowSpacing={4.5} columnSpacing={2.75}>
      <Grid item xs={12}>
        <WelcomeBanner />
      </Grid>
    </Grid>
  );
};

export default Landing;
