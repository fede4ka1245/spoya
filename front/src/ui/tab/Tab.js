import * as React from 'react';
import MuiTab from '@mui/material/Tab';
import { styled } from '@mui/material/styles';

const Tab = styled(MuiTab)(({ theme }) => ({
  textTransform: 'none',
  color: 'var(--hint-color)',
  '&.Mui-selected': {
    color: 'var(--text-primary-color)',
  },
}));

Tab.defaultProps = { disableRipple: true }

export default Tab;