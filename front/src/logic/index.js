export const getDates = () => {
  const generateTabsData = () => {
    const today = new Date();
    const numberOfDays = 10;
    const tabsData = [];

    for (let i = 0; i < numberOfDays; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      const value = formatDate(date); // Use timestamp as label
      tabsData.push(value);
    }

    return tabsData;
  };

  const formatDate = (date) => {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
  };

  return new Promise((res) => {
    res(generateTabsData());
  });
};


export const getEvents = () => {
  return new Promise((res) => {
    res([
      {
        id: 1,
        event: 'My super event',
        probability: 0.3,
        region: 'Uff',
        description: '123s'
      },
      {
        id: 3,
        event: 'Bomb event',
        probability: 0.3,
        region: 'Uff',
        description: '123s'
      },
      {
        id: 8,
        event: 'Fire Fire',
        probability: 0.3,
        region: 'Uff',
        description: '123s'
      },
      {
        id: 12,
        event: 'Go Go',
        probability: 0.3,
        region: 'Uff',
        description: '123s'
      }
    ]);
  });
}