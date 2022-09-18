import { ModalView } from "@slack/bolt";
import { User } from "../model";

// 表示内容と内部情報の対応を辞書形式で保持しておく
const userDepartmentMap = new Map([
  ["its", "ITサービス事業部"],
  ["finance", "金融システム事業部"],
  ["medical", "医療システム事業部"],
  ["agile", "アジャイル事業部"],
  ["etec", "組み込み技術事業部"],
  ["medical-education", "医学教育支援室"],
  ["general", "管理部"],
  ["other", "その他"],
]);
const userJobTypeMap = new Map([
  ["engineer", "開発・導入"],
  ["management", "マネジメント・営業"],
  ["executive", "経営"],
  ["other", "その他"],
]);
const userAgeRangeMap = new Map([
  ["10", "～19才"],
  ["20", "20才～29才"],
  ["30", "30才～39才"],
  ["40", "40才～49才"],
  ["50", "50才～59才"],
  ["60", "60才～"],
]);

/**
 * ユーザプロフィールモーダル
 */
export const userProfileModal = (props: {
  callbackId: string;
  userName: string;
  user?: User;
  privateMetadata?: string;
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    private_metadata: props.privateMetadata,
    title: { type: "plain_text", text: "プロフィール" },
    submit: {
      type: "plain_text",
      text: props.user ? "更新" : "登録",
      emoji: true,
    },
    close: { type: "plain_text", text: "閉じる", emoji: true },
    blocks: [
      {
        type: "section",
        block_id: "section_user_name",
        text: {
          type: "plain_text",
          text: props.userName,
        },
      },
      {
        type: "input",
        block_id: "input_department",
        label: { type: "plain_text", text: "事業部" },
        element: {
          type: "static_select",
          action_id: "department_action",
          placeholder: {
            type: "plain_text",
            text: "事業部を選択してください",
            emoji: true,
          },
          options: Array.from(userDepartmentMap).map((item) => {
            return {
              value: item[0],
              text: { type: "plain_text", text: item[1] },
            };
          }),
        },
      },
      {
        type: "input",
        block_id: "input_job_type",
        label: { type: "plain_text", text: "主な仕事" },
        element: {
          type: "static_select",
          action_id: "job_type_action",
          placeholder: {
            type: "plain_text",
            text: "一番近いものを選択してください",
            emoji: true,
          },
          options: Array.from(userJobTypeMap).map((item) => {
            return {
              value: item[0],
              text: { type: "plain_text", text: item[1] },
            };
          }),
        },
      },
      {
        type: "input",
        block_id: "input_age_range",
        label: { type: "plain_text", text: "年齢層" },
        element: {
          type: "static_select",
          action_id: "age_range_action",
          placeholder: {
            type: "plain_text",
            text: "年齢層を選択してください",
            emoji: true,
          },
          options: Array.from(userAgeRangeMap).map((item) => {
            return {
              value: item[0],
              text: { type: "plain_text", text: item[1] },
            };
          }),
        },
      },
    ],
  };
};
