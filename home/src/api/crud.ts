import { request } from "@/utils/service";

interface QueryParams {
  page?: number;
  pageSize?: number;
  order_by?: string;
}

class Crud {
  protected readonly baseUrl: string;

  constructor(baseUrl: string = "") {
    this.baseUrl = baseUrl || this.constructor.name.toLowerCase();
  }

  /**
   * 获取列表
   * @param query
   * @param filters
   */
  async list(
    query: QueryParams = {
      page: 1,
      pageSize: 10,
      order_by: "-create_time",
    },
    filters = {},
  ): Promise<any> {
    return await request({
      method: "post",
      url: `${this.baseUrl}/list`,
      params: {
        ...query,
      },
      data: filters,
    });
  }

  /**
   * 创建
   * @param data
   */
  async create(data: any): Promise<any> {
    return await request({
      url: `${this.baseUrl}/create`,
      method: "post",
      data,
    });
  }

  /**
   * 批量创建
   * @param data
   */
  async createAll(data: Array<any>): Promise<any> {
    return await request({
      url: `${this.baseUrl}/createAll`,
      method: "post",
      data,
    });
  }

  /**
   * 更新
   * @param id
   * @param data
   */
  async update(id: number, data: any): Promise<any> {
    return await request({
      url: `${this.baseUrl}/${id}`,
      method: "put",
      data,
    });
  }

  /**
   * 删除
   * @param ids
   */
  async delete(ids: string): Promise<any> {
    return await request({
      url: `${this.baseUrl}/${ids}`,
      method: "delete",
    });
  }
}

export default Crud;
