declare namespace Api {
  /** Links management */
  namespace Links {
    interface LinkItem {
      id: number;
      title: string;
      href: string;
      icon?: string;
      is_self: boolean;
      is_vip: boolean;
      desc?: string;
      color?: string;
      order?: number;
      cdn_img_id?: number;
      status: boolean;
      create_time?: string;
      update_time?: string;
      menus?: MenuRelation[];
    }

    interface MenuRelation {
      id: number;
      title: string;
      icon?: string;
      color?: string;
    }

    interface LinkCreate {
      title?: string;
      href?: string;
      icon?: string;
      is_self?: boolean;
      is_vip?: boolean;
      desc?: string;
      color?: string;
      order?: number;
      status?: boolean;
      menus?: number[];
    }

    interface LinkFilter {
      title?: string;
      href?: string;
      status?: boolean | null;
      menus?: number[];
    }

    interface SiteInfo {
      title?: string;
      icon?: string;
      desc?: string;
    }

    interface PageResult {
      items: LinkItem[];
      total: number;
      page: number;
      size: number;
      pages: number;
    }
  }

  /** Nav menu management */
  namespace NavMenu {
    interface MenuItem {
      id: number;
      title: string;
      icon: string;
      order: number;
      color?: string;
      is_vip: boolean;
      status: boolean;
      parent_id?: number | null;
      create_time?: string;
      update_time?: string;
    }

    interface MenuCreate {
      title?: string;
      icon?: string;
      order?: number;
      color?: string;
      is_vip?: boolean;
      status?: boolean;
      parent_id?: number | null;
    }

    interface MenuFilter {
      title?: string;
      status?: boolean | null;
    }

    interface MenuTreeNode extends MenuItem {
      children?: MenuTreeNode[];
      links?: any[];
    }

    interface PageResult {
      items: MenuItem[];
      total: number;
      page: number;
      size: number;
      pages: number;
    }
  }

  /** Friend links management */
  namespace Friend {
    interface FriendItem {
      id: number;
      title: string;
      href: string;
      icon?: string;
      desc?: string;
      color?: string;
      order?: number;
      status: boolean;
      create_time?: string;
      update_time?: string;
    }

    interface FriendCreate {
      title?: string;
      href?: string;
      icon?: string;
      desc?: string;
      color?: string;
      order?: number;
      status?: boolean;
    }

    interface FriendFilter {
      title?: string;
      status?: boolean | null;
    }

    interface PageResult {
      items: FriendItem[];
      total: number;
      page: number;
      size: number;
      pages: number;
    }
  }

  /** System user management */
  namespace SystemUser {
    interface UserItem {
      id: number;
      username: string;
      nickname?: string;
      status: boolean;
      is_super: boolean;
      order?: number;
      create_time?: string;
      update_time?: string;
    }

    interface UserCreate {
      username: string;
      password: string;
      nickname?: string;
      status?: boolean;
      is_super?: boolean;
    }

    interface UserUpdate {
      username?: string;
      nickname?: string;
      status?: boolean;
      password?: string;
      order?: number;
      is_super?: boolean;
    }

    interface UserFilter {
      username?: string;
      status?: boolean | null;
    }

    interface PageResult {
      items: UserItem[];
      total: number;
      page: number;
      size: number;
      pages: number;
    }
  }

  /** Site settings */
  namespace Site {
    interface SiteInfo {
      id: number;
      title: string;
      desc?: string;
      keywords?: string;
      icon?: string;
      color?: string;
      footer?: string;
      yiyan: boolean;
      weather: boolean;
      weather_key?: string;
      copyright?: string;
      cdn_img_token?: string;
      status: boolean;
    }

    interface SiteUpdate {
      id?: number;
      title?: string;
      desc?: string;
      keywords?: string;
      icon?: string;
      color?: string;
      footer?: string;
      yiyan?: boolean;
      weather?: boolean;
      weather_key?: string;
      copyright?: string;
      cdn_img_token?: string;
    }
  }

  /** CORS origin management */
  namespace CorsOrigin {
    interface CorsItem {
      id: number;
      origin: string;
      desc?: string;
      order?: number;
      status: boolean;
      create_time?: string;
      update_time?: string;
    }

    interface CorsCreate {
      origin: string;
      desc?: string;
      order?: number;
      status?: boolean;
    }

    interface CorsFilter {
      origin?: string;
      status?: boolean | null;
    }

    interface PageResult {
      items: CorsItem[];
      total: number;
      page: number;
      size: number;
      pages: number;
    }
  }
}
