import { request } from "@/utils/service"

class Crud {
  protected readonly baseUrl: string

  constructor(baseUrl: string = "") {
    this.baseUrl = baseUrl || this.constructor.name.toLowerCase()
  }

  /**
   * 获取列表
   * @param page
   * @param pageSize
   * @param filters
   */
  async list(page: number = 1, pageSize: number = 10, filters = {}): Promise<any> {
    return await request({
      url: `${this.baseUrl}/list`,
      method: "post",
      params: {
        page: page,
        size: pageSize
      },
      data: filters
    })
  }

  /**
   * 创建
   * @param data
   */
  async create(data: any): Promise<any> {
    return await request({
      method: "post",
      url: `${this.baseUrl}/create`,
      data
    })
  }

  /**
   * 批量创建
   * @param data
   */
  async createAll(data: Array<any>): Promise<any> {
    return await request({
      method: "post",
      url: `${this.baseUrl}/create/all`,
      data
    })
  }

  /**
   * 更新
   * @param id
   * @param data
   */
  async update(id: number, data: any): Promise<any> {
    return await request({
      method: "put",
      url: `${this.baseUrl}/${id}`,
      data
    })
  }

  /**
   * 删除
   * @param ids
   */
  async delete(ids: string): Promise<any> {
    return await request({
      method: "delete",
      url: `${this.baseUrl}/${ids}`
    })
  }
}

export default Crud
