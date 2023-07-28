export interface MenuType {
  id: number;
  title: string;
  icon: string;
  nav?: ItemType[];
  children?: MenuType[];
}

export interface ItemType {
  title: string;
  href: string;
  icon?: string;
  isSelf?: boolean;
  desc?: string;
}
