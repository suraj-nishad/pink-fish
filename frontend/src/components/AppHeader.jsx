import {
  Header,
  HeaderName,
  HeaderNavigation,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
} from '@carbon/react';
import { Notification, UserAvatar, Switcher } from '@carbon/icons-react';
import './AppHeader.scss';

const AppHeader = () => {
  return (
    <Header aria-label="PlantOps Digital Twin">
      <HeaderName href="/" prefix="IBM">
        <span className="header-title">PlantOps Digital Twin</span>
      </HeaderName>
      
      <HeaderNavigation aria-label="Main Navigation">
        <HeaderMenuItem href="/">Dashboard</HeaderMenuItem>
        <HeaderMenuItem href="/simulation">Simulation</HeaderMenuItem>
        <HeaderMenuItem href="/analytics">Analytics</HeaderMenuItem>
      </HeaderNavigation>

      <HeaderGlobalBar>
        <HeaderGlobalAction
          aria-label="Notifications"
          tooltipAlignment="end"
        >
          <Notification size={20} />
        </HeaderGlobalAction>
        <HeaderGlobalAction
          aria-label="App Switcher"
          tooltipAlignment="end"
        >
          <Switcher size={20} />
        </HeaderGlobalAction>
        <HeaderGlobalAction
          aria-label="User Profile"
          tooltipAlignment="end"
        >
          <UserAvatar size={20} />
        </HeaderGlobalAction>
      </HeaderGlobalBar>
    </Header>
  );
};

export default AppHeader;
