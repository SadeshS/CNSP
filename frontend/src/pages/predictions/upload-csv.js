import { useNavigate } from 'react-router';

// material-ui
import { Button, Grid, Stack, FormHelperText } from '@mui/material';

// project-imports
import MainCard from 'components/MainCard';
import UploadSingleFile from 'components/third-party/dropzone/SingleFile';
import AnimateButton from 'components/@extended/AnimateButton';
import useAuth from 'hooks/useAuth';
import { dispatch } from 'store';
import { openSnackbar } from 'store/reducers/snackbar';
import axiosService from 'utils/axios';

// third-party
import { Formik } from 'formik';
import * as yup from 'yup';

const UploadCSV = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  return (
    <Grid>
      <Grid item xs={12}>
        <MainCard title="Upload Your Transactional Data CSV File">
          <Formik
            initialValues={{ files: null }}
            onSubmit={async (values) => {
              try {
                if (values.files.length > 0) {
                  const formData = new FormData();
                  formData.append('file', values.files[0]);
                  const response = await axiosService.post(`/predictions/predict/${user.id}`, formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data'
                    }
                  });

                  dispatch(
                    openSnackbar({
                      open: true,
                      message: response.data.message,
                      variant: 'alert',
                      alert: {
                        color: 'success'
                      },
                      close: true
                    })
                  );

                  navigate('/');
                }
              } catch (error) {
                dispatch(
                  openSnackbar({
                    open: true,
                    message: 'Error while uploading the csv file. Please try again later.',
                    variant: 'alert',
                    alert: {
                      color: 'error'
                    },
                    close: true
                  })
                );
              }
            }}
            validationSchema={yup.object().shape({
              files: yup.mixed().required('CSV file is required.')
            })}
          >
            {({ values, handleSubmit, setFieldValue, touched, errors }) => (
              <form onSubmit={handleSubmit}>
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <Stack spacing={1.5} alignItems="center">
                      <UploadSingleFile
                        showList={false}
                        setFieldValue={setFieldValue}
                        files={values.files}
                        error={touched.files && !!errors.files}
                      />
                      {touched.files && errors.files && (
                        <FormHelperText error id="standard-weight-helper-text-password-login">
                          {errors.files}
                        </FormHelperText>
                      )}

                      <Stack alignItems="flex-end" width="100%">
                        <AnimateButton>
                          <Button variant="contained" sx={{ my: 3, ml: 1 }} type="submit" disabled={values.files === null}>
                            Predict
                          </Button>
                        </AnimateButton>
                      </Stack>
                    </Stack>
                  </Grid>
                </Grid>
              </form>
            )}
          </Formik>
        </MainCard>
      </Grid>
    </Grid>
  );
};

export default UploadCSV;
