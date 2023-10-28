import React from 'react';
import {Backdrop, CircularProgress, Grid} from "@mui/material";

const AppLoader = ({ loading }) => {
  return (
    <>
      <Backdrop
        sx={{ color: '#fff', zIndex: 1001 }}
        open={loading}
        onClick={() => {}}
      >
        <Grid
          width={'90px'}
          height={'90px'}
          display={'flex'}
          flexDirection={'column'}
          justifyContent={'center'}
          alignItems={'center'}
          backgroundColor={'var(--bg-color)'}
          border={'var(--element-border)'}
          position={'relative'}
          borderRadius={'var(--border-radius-lg)'}
        >
          <CircularProgress
            sx={{
              color: 'var(--primary-color)'
            }}
          />
        </Grid>
      </Backdrop>
    </>
  );
};

export default AppLoader;