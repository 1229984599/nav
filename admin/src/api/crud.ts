import { request } from "@/utils/request";

export interface QueryParams {
  page?: number;
  size?: number;
  order_by?: string;
}

class Crud {
  public readonly baseUrl: string;
  protected defaultQueryParams: QueryParams;

  constructor(baseUrl: string = "") {
    this.baseUrl = baseUrl || this.constructor.name.toLowerCase();
    this.defaultQueryParams = {
      page: 1,
      size: 10,
      order_by: "-create_time",
    };
  }

  /**
   * 获取列表
   * @param query
   * @param filters
   */
  async list(query: QueryParams = {}, filters = {}): Promise<any> {
    const queryParams = Object.assign(this.defaultQueryParams, query);
    return await request({
      method: "post",
      url: `${this.baseUrl}/list`,
      params: {
        ...queryParams,
      },
      data: filters,
    });
  }

  /**
   *  获取详情
   * @param id
   */
  async read(id: number): Promise<any> {
    return await request({
      url: `${this.baseUrl}/read/${id}`,
      method: "get",
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

export function useRequest(model: Crud) {
  const pageRequest = async (query: any) => {
    return await model.list(query.params, query.filters);
  };
  const editRequest = async ({ form, row }: any) => {
    form.id = row.id;
    return await model.update(row.id, form);
  };
  const delRequest = async ({ row }: any) => {
    return await model.delete(row.id);
  };

  const addRequest = async ({ form }: any) => {
    return await model.create(form);
  };
  return {
    pageRequest,
    addRequest,
    editRequest,
    delRequest,
  };
}

export default Crud;
