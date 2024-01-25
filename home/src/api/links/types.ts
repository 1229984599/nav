/**
 * Page_LinkSchemaList_
 */
export interface PageLinkSchemaList {
    /**
     * Items
     */
    items: LinkSchemaList[];
    /**
     * Page
     */
    page?: number;
    /**
     * Pages
     */
    pages?: number;
    /**
     * Size
     */
    size?: number;
    /**
     * Total
     */
    total: number;
}

/**
 * LinkSchemaList
 */
export interface LinkSchemaList {
    color?: string;
    created?: Date;
    desc?: string;
    href?: string;
    icon?: string;
    id?: number;
    is_self?: boolean;
    status?: boolean;
    is_vip?: boolean;
    menus: MenuSchemaRelation[];
    order?: number;
    title?: string;
    updated?: Date;
}

/**
 * MenuSchemaRelation
 */
export interface MenuSchemaRelation {
    /**
     * Id
     */
    id?: number;
    /**
     * Title
     */
    title?: string;
}

/**
 * SiteInfo
 */
export interface SiteInfo {
    title?: string;
    icon?: string;
    desc?: string;
}

/**
 * LinksSchemaFilters
 */
export interface LinksSchemaFilters {
    /**
     * Title
     */
    title?: string;
    status?: boolean;
}

/**
 * CreateMenuSchema
 */
export interface CreateMenuSchema {
    /**
     * Color，图标颜色hex
     */
    color?: string;
    /**
     * Desc
     */
    desc?: string;
    /**
     * Href
     */
    href?: string;
    /**
     * Icon
     */
    icon?: string;
    /**
     * Is Self
     */
    is_self?: boolean;
    /**
     * Menus
     */
    menus?: number[];
    /**
     * Order，值越大越靠前
     */
    order?: number | null;
    /**
     * Title
     */
    title?: string;
}
