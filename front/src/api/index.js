export const getDistricts = () => {
  return fetch(`${process.env.REACT_APP_API}/get-districts`)
    .then((res) => res.json());
};

export const getDates = () => {
  return fetch(`${process.env.REACT_APP_API}/get-latest-dates`)
    .then((res) => res.json());
};

export const getEventTypes = () => {
  return fetch(`${process.env.REACT_APP_API}/get-events-types`)
    .then((res) => res.json())
    .then((events) => events.filter((name) => name !== 'Нет события'));
};

export const getEvents = (type, date) => {
  return fetch(`${process.env.REACT_APP_API}/get-events?type=${type}&date=${date}`)
    .then((res) => res.json());
};