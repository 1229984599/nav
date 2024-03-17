// 获取热搜
export interface HotItemType {
  hot: string;
  title: string;
  updatetime: string;
  url: string;
}

// 和风天气现在数据
export interface WeatherType {
  obsTime?: string;
  temp?: string;
  feelsLike?: string;
  icon?: string;
  text?: string;
  wind360?: string;
  windDir?: string;
  windScale?: string;
  windSpeed?: string;
  humidity?: string;
  precip?: string;
  pressure?: string;
  vis?: string;
  cloud?: string;
  dew?: string;
}

/*
 * 和风天气后台返回数据（未来七天）
 */
export interface FutureWeatherType {
  fxDate?: string;
  sunrise?: string;
  sunset?: string;
  moonrise?: string;
  moonset?: string;
  moonPhase?: string;
  moonPhaseIcon?: string;
  tempMax?: string;
  tempMin?: string;
  iconDay?: string;
  textDay?: string;
  iconNight?: string;
  textNight?: string;
  wind360Day?: string;
  windDirDay?: string;
  windScaleDay?: string;
  windSpeedDay?: string;
  wind360Night?: string;
  windDirNight?: string;
  windScaleNight?: string;
  windSpeedNight?: string;
  humidity?: string;
  precip?: string;
  pressure?: string;
  vis?: string;
  cloud?: string;
  uvIndex?: string;
}

// 和风天气后台返回数据
export interface WeatherRespType {
  city: string;
  weather: WeatherType;
  future_weather: FutureWeatherType[];
}
