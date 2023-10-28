import React, {useCallback} from 'react';
import Tabs from "../../ui/tabs/Tabs";
import Tab from "../../ui/tab/Tab";
import {useDispatch, useSelector} from "react-redux";
import {setDate} from "../../store";

const Dates = () => {
  const { dates, date } = useSelector((state) => state.main);
  const dispatch = useDispatch();

  const onTargetTabSet = useCallback((_, newValue) => {
    dispatch(setDate(newValue))
  }, []);

  return (
    <>
      <Tabs
        value={date}
        onChange={onTargetTabSet}
        aria-label="date-tabs"
        variant="scrollable"
        scrollButtons
        allowScrollButtonsMobile
      >
        {dates.map((date) => (
          <Tab key={date} label={date} value={date} />
        ))}
      </Tabs>
    </>
  );
};

export default Dates;