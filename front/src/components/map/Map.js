import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import {initMap, loadDistrictsEvents} from "../../store";
import {Grid, Typography} from "@mui/material";

const getColor = (probability) => {
  if (probability <= 30) {
    return 'var(--map-success-color)';
  } else if (probability > 30 && probability <= 54) {
    return 'var(--map-warn-color-1)';
  } else if (probability > 55 && probability <= 70) {
    return 'var(--map-warn-color-2)';
  } else {
    return 'var(--map-danger-color)';
  }
}

const Legend = () => {

  return (
    <Grid display={'flex'} flexDirection={'column'}>
      <Grid display={'flex'} alignItems={'center'}>
        <Typography
          fontWeight={'bold'}
          fontSize={'14px'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--text-secondary-color)'}
          mb={'5px'}
        >
          Уровни риска
        </Typography>
      </Grid>
      <Grid display={'flex'} alignItems={'center'}>
        <Grid
          backgroundColor={'var(--map-success-color)'}
          width={'8px'}
          height={'8px'}
          borderRadius={'50%'}
        />
        <Typography
          fontWeight={'bold'}
          fontSize={'11px'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--hint-color)'}
          ml={'5px'}
        >
          - Низкий
        </Typography>
      </Grid>
      <Grid display={'flex'} alignItems={'center'}>
        <Grid
          backgroundColor={'var(--map-warn-color-1)'}
          width={'8px'}
          height={'8px'}
          borderRadius={'50%'}
        />
        <Typography
          fontWeight={'bold'}
          fontSize={'11px'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--hint-color)'}
          ml={'5px'}
        >
          - Умеренный
        </Typography>
      </Grid>
      <Grid display={'flex'} alignItems={'center'}>
        <Grid
          backgroundColor={'var(--map-warn-color-2)'}
          width={'8px'}
          height={'8px'}
          borderRadius={'50%'}
        />
        <Typography
          fontWeight={'bold'}
          fontSize={'11px'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--hint-color)'}
          ml={'5px'}
        >
          - Повышенный
        </Typography>
      </Grid>
      <Grid display={'flex'} alignItems={'center'}>
        <Grid
          backgroundColor={'var(--map-danger-color)'}
          width={'8px'}
          height={'8px'}
          borderRadius={'50%'}
        />
        <Typography
          fontWeight={'bold'}
          fontSize={'11px'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--hint-color)'}
          ml={'5px'}
        >
          - Высокий
        </Typography>
      </Grid>
      <Grid display={'flex'} alignItems={'center'}>
        <Grid
          backgroundColor={'var(--map-no-data-color)'}
          width={'8px'}
          height={'8px'}
          borderRadius={'50%'}
        />
        <Typography
          fontWeight={'bold'}
          fontSize={'11px'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--hint-color)'}
          ml={'5px'}
        >
          - Нет данных
        </Typography>
      </Grid>
    </Grid>
  )
}

function MyHint() {
  const { hint, reactify } = useSelector((state) => state.main);

  const { YMapHintContext } = useMemo(() => {
    if (reactify?.module && hint) {
      return reactify.module(hint);
    }

    return {};
  }, [hint, reactify]);

  const ctx = React.useContext(YMapHintContext, [YMapHintContext]);

  if (!YMapHintContext || !ctx?.hint) {
    return null;
  }

  return (
    <>
      <Grid
        border={'var(--element-border)'}
        overflow={'hidden'}
        borderRadius={'var(--border-radius-sm)'}
        backgroundColor={'var(--secondary-bg-color)'}
        p={'var(--space-md)'}
        width={'17em'}
        minHeight={'12em'}
        sx={{ transform: 'translate(0, -100%)' }}
      >
        <Typography
          fontWeight={'bold'}
          fontSize={'var(--font-size-sm)'}
          lineHeight={'var(--font-size-sm)'}
          color={'var(--text-secondary-color)'}
        >
          {ctx?.hint?.name}
        </Typography>
        {ctx?.hint?.description === 'no-data' && (
          <Typography
            pt={'var(--space-md)'}
            fontSize={'22px'}
            lineHeight={'22px'}
            fontWeight={'bold'}
            color={'var(--hint-color)'}
          >
            Нет данных!
          </Typography>
        )}
        {ctx?.hint?.description !== 'no-data' && (
          <>
            <Typography
              pt={'var(--space-sm)'}
              fontSize={'15px'}
              lineHeight={'16px'}
              color={'var(--text-secondary-color)'}
            >
              <strong>Признаки:</strong> {ctx?.hint?.description}
            </Typography>
            <Typography
              pt={'var(--space-sm)'}
              fontSize={'15px'}
              lineHeight={'16px'}
              color={getColor(ctx?.hint?.probability)}
            >
              <strong>Вероятность:</strong> {ctx?.hint?.probability}%
            </Typography>
          </>
        )}
      </Grid>
    </>
  );
}

const Map = () => {
  const [location, setLocation] = useState({center: [56.25017, 58.01046], zoom: 7});
  const { isMapReady, components, hint, reactify, districts, eventId, date } = useSelector((state) => state.main);
  const [features, setFeatures] = useState([]);
  const dispatch = useDispatch();
  const {
    YMap,
    YMapDefaultSchemeLayer,
    YMapDefaultFeaturesLayer,
    YMapFeature,
    YMapControls,
    YMapListener,
    YMapZoomControl,
    YMapGeolocationControl,
    YMapCollection
  } = useMemo(() => {
    return components;
  }, [components]);

  const { YMapHint } = useMemo(() => {
    if (reactify?.module && hint) {
      return reactify.module(hint)
    }

    return {};
  }, [hint, reactify]);

  const onUpdate = React.useCallback(({location, mapInAction}) => {
    // Animation not happening
    if (!mapInAction) {
      setLocation({
        center: location.center,
        zoom: location.zoom
      });
    }
  }, []);

  useEffect(() => {
    if (!isMapReady || !YMap || !YMapHint || !districts.length) {
      return;
    }

    const features = [...districts.map(({ geometry, name, osm_id, description, probability }) => {
      return {
        id: String(osm_id),
        draggable: false,
        geometry: geometry,
        properties: {
          hint: {
            name,
            description: description ?? 'no-data',
            probability: probability ?? null
          }
        },
        style: {
          fillRule: 'nonZero',
          fill: description ? getColor(probability) : 'var(--map-no-data-color)',
          fillOpacity: 0.6,
          stroke: [
            {
              color: description ? getColor(probability) : 'var(--map-no-data-color)',
              width: 5,
            }
          ]
        }
      };
    })];

    setFeatures(features);
  }, [isMapReady, YMap, districts]);

  useEffect(() => {
    dispatch(initMap());
  }, []);

  useEffect(() => {
    if (eventId && date) {
      dispatch(loadDistrictsEvents({ type: eventId, date }))
    }
  }, [eventId, date]);

  const getHint = useCallback((object) => object?.properties?.hint, []);

  if (!isMapReady || !YMap || !YMapHint) {
    return null;
  }

  return (
    <>
      <Grid
        position={'absolute'}
        left={0}
        top={0}
        border={'var(--element-border)'}
        overflow={'hidden'}
        borderRadius={'var(--border-radius-sm)'}
        backgroundColor={'var(--secondary-bg-color)'}
        zIndex={1000}
        p={'var(--space-md)'}
      >
        <Legend />
      </Grid>
      <YMap location={location}>
        <YMapDefaultSchemeLayer />
        <YMapDefaultFeaturesLayer />
        <YMapListener onUpdate={onUpdate} />
        <YMapControls position="bottom">
          <YMapZoomControl />
        </YMapControls>
        <YMapControls position="bottom left">
          <YMapGeolocationControl />
        </YMapControls>
        <YMapHint hint={getHint}>
          <MyHint />
        </YMapHint>
        <YMapCollection>
          {features.map((feature) => (
            <YMapFeature key={feature.id} {...feature} />
          ))}
        </YMapCollection>
        {features.map((feature) => (
          <YMapFeature
            key={feature.id}
            {...feature}
          />
        ))}
      </YMap>
    </>
  );
};

export default Map;