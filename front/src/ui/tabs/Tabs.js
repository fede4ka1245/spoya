import * as React from 'react';
import MuiTabs from '@mui/material/Tabs';
import { styled } from '@mui/material/styles';

const Tabs = styled(MuiTabs)(({ theme }) => ({
  '& .MuiTabs-indicator': {
    backgroundColor: 'var(--primary-color)',
    height: '3px',
    borderRadius: '4px 4px 0 0'
  },
  '& .MuiTabs-scrollButtons': {
    color: 'var(--hint-color)',
  },
}));

export default Tabs;