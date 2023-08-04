export interface catItemType {
  id?: number;
  title: string;
  href: string;
}

export interface catSearchType {
  id: number;
  href?: string;
  title: string;
  is_self?: boolean;
  children?: catItemType[];
}

export const catSearchList: catSearchType[] = [
  {
    id: 1,
    title: "站内",
    href: "/search?kw=",
  },
  {
    id: 2,
    title: "搜索",
    children: [
      {
        title: "百度",
        href: "https://www.baidu.com/s?ie=UTF-8&wd=",
      },
      {
        title: "360",
        href: "https://www.so.com/s?ie=utf-8&q=",
      },
    ],
  },
  {
    id: 3,
    title: "视频",
    href: "https://movie2.moxiaoying.top/search.php?cat=search.php&searchword=",
  },
];
