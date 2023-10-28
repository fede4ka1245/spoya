import React, {useEffect} from 'react';
import {Grid, Typography} from "@mui/material";
import Dates from "./components/dates/Dates";
import Map from "./components/map/Map";
import Events from "./components/events/Events";
import {useDispatch, useSelector} from "react-redux";
import AppLoader from "./ui/appLoader/AppLoader";
import {initApp} from "./store";

const Root = () => {
  const { isLoading } = useSelector((state) => state.main);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(initApp());
  }, []);

  return (
    <>
      <AppLoader loading={isLoading} />
      <div className={'app-container'}>
        <div className={'app-container-content-1'}>
          <div className={'app-container-header'}>
            <Typography
              pl={'var(--space-md)'}
              pr={'var(--space-md)'}
              color={'var(--text-secondary-color)'}
              fontWeight={'bold'}
              fontSize={'var(--font-size-md)'}
            >
              СПОНЯ
            </Typography>
          </div>
          <div className={'app-container-dates'}>
            <Grid
              border={'var(--element-border)'}
              overflow={'hidden'}
              borderRadius={'var(--border-radius-lg)'}
              backgroundColor={'var(--bg-color)'}
              mt={'var(--space-sm)'}
              ml={'var(--space-sm)'}
              mr={'var(--space-sm)'}
            >
              <Dates />
            </Grid>
          </div>
          <div className={'app-container-map'}>
            <Grid
              border={'var(--element-border)'}
              height={'100%'}
              overflow={'hidden'}
              borderRadius={'var(--border-radius-lg)'}
              backgroundColor={'var(--bg-color)'}
              position={'relative'}
            >
              <Map />
            </Grid>
          </div>
        </div>
        <div className={'app-container-content-2'}>
          <Events />
        </div>
      </div>
    </>
  );
};

export default Root;