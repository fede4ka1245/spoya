import {configureStore, createAsyncThunk} from '@reduxjs/toolkit';
import React from 'react';
import ReactDOM from 'react-dom';
import { createSlice } from '@reduxjs/toolkit';
import {getDistricts, getDates, getEventTypes, getEvents} from "../api";

const initialState = {
  eventId: undefined,
  events: [],
  date: undefined,
  dates: [],
  districts: [],
  yaMap: undefined,
  components: {},
  isMapReady: false,
  isLoading: false,
  hint: undefined,
  reactify: undefined,
  districtsEvents: []
};

const initMap = createAsyncThunk(
  'main/initMap',
  async () => {
    const script = document.createElement('script');
    document.body.appendChild(script);
    script.type = "text/javascript";
    script.src = `https://api-maps.yandex.ru/v3/?apikey=${process.env.REACT_APP_YANDEX_MAP_KEY}&lang=ru_RU`;

    return new Promise((res) => {
      script.onload = async () => {
        await window.ymaps3.ready;
        const controls = await window.ymaps3.import('@yandex/ymaps3-controls@0.0.1');
        const hint = await window.ymaps3.import('@yandex/ymaps3-hint@0.0.1');
        const ymaps3Reactify = await window.ymaps3.import('@yandex/ymaps3-reactify');
        const reactify = ymaps3Reactify.reactify.bindTo(React, ReactDOM);

        const {
          YMap,
          YMapDefaultSchemeLayer,
          YMapDefaultFeaturesLayer,
          YMapFeature,
          YMapControls,
          YMapListener,
          YMapCollection
        } = reactify.module(window.ymaps3);

        const components = {
          YMap,
          YMapDefaultSchemeLayer,
          YMapDefaultFeaturesLayer,
          YMapFeature,
          YMapControls,
          YMapListener,
          YMapCollection,
          ...reactify.module(controls)
        };

        res({
          yaMap: window.ymaps3,
          isMapReady: true,
          reactify,
          hint,
          controls,
          components,
        });
      }
    })
  }
);

const initApp = createAsyncThunk(
  'main/initApp',
  async () => {
    const dates = await getDates();
    const events = await getEventTypes();
    const districts = await getDistricts();

    return {
      dates,
      events,
      districts
    }
  }
);

const loadDistrictsEvents = createAsyncThunk(
  'main/loadDistrictsEvents',
  async ({ type, date }) => {
    const districtsEvents = await getEvents(type, date);

    return {
      districtsEvents
    }
  }
);

export const mainSlice = createSlice({
  name: 'main',
  initialState,
  reducers: {
    setDate: (state, action) => {
      state.date = action.payload;
    },
    setEvent: (state, action) => {
      state.eventId = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder.addCase(initMap.fulfilled, (state, action) => {
      const {
        yaMap,
        isMapReady,
        components,
        reactify,
        hint
      } = action.payload;

      state.isMapReady = isMapReady;
      state.yaMap = yaMap;
      state.components = components;
      state.reactify = reactify;
      state.hint = hint;
    });
    builder.addCase(initApp.pending, (state) => {
      state.isLoading = true;
    });
    builder.addCase(loadDistrictsEvents.pending, (state) => {
      state.isLoading = true;
    });
    builder.addCase(loadDistrictsEvents.fulfilled, (state, action) => {
      const { districtsEvents } = action.payload;

      state.isLoading = false;

      if (state.districts.length) {
        state.districts = state.districts.map((district) => {
          const targetEvent = districtsEvents[district.name];

          return {
            ...district,
            description: targetEvent?.description ?? '-',
            probability: ((targetEvent?.probability ?? 0) * 100).toFixed(0)
          };
        });
      }
    });
    builder.addCase(initApp.fulfilled, (state, action) => {
      const {
        dates,
        events,
        districts
      } = action.payload;

      state.isLoading = false;
      state.districts = districts;
      state.dates = dates;
      state.events = events;
      state.date = dates[0];
    });
  }
})

const {
  setDate,
  setEvent
} = mainSlice.actions;

export {
  setDate,
  setEvent,
  initMap,
  initApp,
  loadDistrictsEvents
};

export default configureStore({
  reducer: {
    main: mainSlice.reducer,
  }
});