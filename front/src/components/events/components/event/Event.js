import React, {useCallback, useMemo} from 'react';
import styles from './Event.module.css';
import {Typography} from "@mui/material";
import classNames from "classnames";
import {useDispatch, useSelector} from "react-redux";
import {setEvent} from "../../../../store";

const Event = ({ event }) => {
  const { eventId } = useSelector((state) => state.main);
  const dispatch = useDispatch();

  const isActive = useMemo(() => {
    return event === eventId;
  }, [event, eventId]);

  const onClick = useCallback(() => {
    dispatch(setEvent(event));
  }, [event]);

  return (
    <div onClick={onClick} className={classNames(styles.main, {[styles.active]: isActive})}>
      <Typography
        fontWeight={'bold'}
        fontSize={'var(--font-size-sm)'}
        p={'var(--space-sm)'}
      >
        {event}
      </Typography>
    </div>
  );
};

export default Event;