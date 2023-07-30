import { http } from "@/utils/http";

class Crud {
  protected readonly baseUrl: string;

  constructor(baseUrl: string = "") {
    this.baseUrl = baseUrl || this.constructor.name.toLowerCase();
  }

  /**
   * 获取列表
   * @param page
   * @param pageSize
   * @param filters
   */
  async list(
    page: number = 1,
    pageSize: number = 10,
    filters = {}
  ): Promise<any> {
    return await http.post(`${this.baseUrl}/list`, {
      params: {
        page: page,
        size: pageSize
      },
      data: filters
    });
  }

  /**
   * 创建
   * @param data
   */
  async create(data: any): Promise<any> {
    return await http.post(`${this.baseUrl}/create`, { data });
  }

  /**
   * 批量创建
   * @param data
   */
  async createAll(data: Array<any>): Promise<any> {
    return await http.post(`${this.baseUrl}/create/all`, { data });
  }

  /**
   * 更新
   * @param id
   * @param data
   */
  async update(id: number, data: any): Promise<any> {
    return await http.request("put", `${this.baseUrl}/${id}`, { data });
  }

  /**
   * 删除
   * @param ids
   */
  async delete(ids: string): Promise<any> {
    return await http.request("delete", `${this.baseUrl}/${ids}`);
  }
}

export function useRequest(model: Crud) {
  const pageRequest = async query => {
    return await model.list(query.page, query.pageSize, query.filters);
  };
  const editRequest = async ({ form, row }) => {
    form.id = row.id;
    return await model.update(row.id, form);
  };
  const delRequest = async ({ row }) => {
    return await model.delete(row.id);
  };

  const addRequest = async ({ form }) => {
    return await model.create(form);
  };
  return {
    pageRequest,
    addRequest,
    editRequest,
    delRequest
  };
}

export default Crud;
