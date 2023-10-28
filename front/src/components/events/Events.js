import React from 'react';
import {Grid, Typography} from "@mui/material";
import Event from "./components/event/Event";
import {useSelector} from "react-redux";

const Events = () => {
  const { events } = useSelector((state) => state.main);

  return (
    <Grid
      height={'100%'}
      bgcolor={'var(--bg-color)'}
      borderLeft={'var(--element-border)'}
      display={'flex'}
      flexDirection={'column'}
    >
      <Typography
        p={'var(--space-md)'}
        color={'var(--text-secondary-color)'}
        fontWeight={'bold'}
        fontSize={'var(--font-size-md)'}
      >
        Явления
      </Typography>
      <Grid flex={1} sx={{ overflowY: 'scroll' }}>
        {events.map((event) => (
          <Event
            key={event.id}
            event={event}
          />
        ))}
      </Grid>
    </Grid>
  );
};

export default Events;