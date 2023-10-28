import React from 'react';
import styles from './Tappable.module.css';

const Tappable = ({ children, onClick }) => {
  return (
    <div className={styles.main} onClick={onClick}>
      { children }
    </div>
  );
};

export default Tappable;